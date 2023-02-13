#![allow(non_snake_case)]

use std::{env, str, path::Path, fs::File, string::String};
use std::process::{exit, Command};
use std::io::{self, BufRead};
use lazy_static::lazy_static;
use regex::Regex;

const EXIT_SUCCESS: i32 = 0;
const EXIT_FAILURE: i32 = 1;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        eprintln!("Not enough arguments");
        exit(EXIT_FAILURE);
    }

    match parse_url_file(args[1].as_str()) {
        Ok(urls) => {
            let mut outputs: Vec<(String, i64)> = Vec::new();

            match get_token() {
                Ok(token) => {
                    for url in urls.iter() {
                        match get_package(&url) {
                            Ok((owner, repo)) => {
                                match get_package_scores(
                                    &owner, &repo, token.as_str()
                                ) {
                                    Ok(package_scores) => {
                                        outputs.push((
                                            String::from(format!(
                                                "{} {:.prec$} {:.prec$} {:.prec$} {:.prec$} {:.prec$} {:.prec$}",
                                                url,
                                                package_scores[5],
                                                package_scores[0],
                                                package_scores[1],
                                                package_scores[2],
                                                package_scores[3],
                                                package_scores[4],
                                                prec = 2,
                                            )), 
                                            ((package_scores[5] * 1000.0).round() as i32).into()
                                        ));
                                    },
                                    Err(err) => {
                                        eprintln!("{}", err);
                                        exit(EXIT_FAILURE);
                                    }
                                }
                            },
                            Err(err) => {
                                eprintln!("{}", err);
                                exit(EXIT_FAILURE);
                            }
                        }
                    }
                    // sort packages by net score
                    outputs.sort_by_key(|key| key.1);

                    println!("URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE");
                    for output in outputs.iter() {
                        println!("{}", output.0);
                    }
                    exit(EXIT_SUCCESS);
                },
                Err(err) => {
                    eprintln!("{}", err);
                    exit(EXIT_FAILURE);
                }
            }        
        },
        Err(err) => {
            eprintln!("{}", err);
            exit(EXIT_FAILURE);
        }
    }
}

fn parse_url_file(url_file: &str) -> Result<Vec<String>, &'static str> {
    // Check to see if file exists
    if Path::new(url_file).exists() {
        let mut urls: Vec<String> = Vec::new();

        // Read URLs from file
        if let Ok(lines) = read_lines(url_file) {
            for line in lines {
                if let Ok(url) = line {
                    urls.push(url);
                }
            }
        }

        return Ok(urls);

    } else {
        return Err("Cannot access file...try checking file permissions");
    }
}

fn get_token() -> Result<String, &'static str> {
    if let Ok(token) = env::var("GITHUB_TOKEN") {
        return Ok(token);
    } else {
        return Err("Cannot access environment variable $GITHUB_TOKEN");
    }
}

fn get_package(url: &str) -> Result<(String, String), &'static str> {
    match parse_url(url) {
        Ok((owner, repo)) => return Ok((owner, repo)),
        Err(err) => return Err(err)
    }
}

fn parse_url(url: &str) -> Result<(String, String), &'static str> {
    // Determine source
    lazy_static! {
        static ref RE: Regex = Regex::new(
            r"\S*(github.com|npmjs.com)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-_.]+)"
        ).unwrap();
    }

    if let Some(captures) = RE.captures(url) {
        let source = String::from(&captures[1]);
        let owner = String::from(&captures[2]);
        let repo = String::from(&captures[3]);

        if source.eq("npmjs.com") {
            match npm_to_git(&repo) {
                Ok(owner) => return Ok((owner, repo)),
                Err(err) => return Err(err)
            }
        }
        return Ok((owner, repo));
    } else {
        return Err("Invalid URL");
    }
}

fn get_package_scores(owner: &str, repo: &str, token: &str) -> Result<Vec<f64>, &'static str> {
    let mut package_scores: Vec<f64> = Vec::new();

    let ramp_up_score: f64;
    let correctness_score: f64;
    let bus_factor_score: f64;
    let responsive_maintainer_score: f64;
    let license_score: f64;

    let mut result: Result<f64, &'static str>;

    result = get_ramp_up_score(owner, repo, token);
    match result {
        Ok(score) => {
            ramp_up_score = score;
        },
        Err(err) => return Err(err)
    }

    result = get_responsive_maintainer_score(owner, repo, token);
    match result {
        Ok(score) => {
            responsive_maintainer_score = score;
        },
        Err(err) => return Err(err)
    }

    result = get_correctness_score(owner, repo, token, responsive_maintainer_score);
    match result {
        Ok(score) => {
            correctness_score = score;
        },
        Err(err) => return Err(err)
    }

    result = get_bus_factor_score(owner, repo, token);
    match result {
        Ok(score) => {
            bus_factor_score = score;
        },
        Err(err) => return Err(err)
    }

    result = get_license_score(owner, repo, token);
    match result {
        Ok(score) => {
            license_score = score;
        },
        Err(err) => return Err(err)
    }

    package_scores.push(ramp_up_score);
    package_scores.push(correctness_score);
    package_scores.push(bus_factor_score);
    package_scores.push(responsive_maintainer_score);
    package_scores.push(license_score);
    package_scores.push(net_score(
        ramp_up_score,
        correctness_score,
        bus_factor_score,
        responsive_maintainer_score,
        license_score
    ));

    return Ok(package_scores);
}

fn npm_to_git(repo: &str) -> Result<String, &'static str> {
    if let Ok(py_output) = Command::new("python3")
                                   .arg("src/url/url.py")
                                   .arg(repo)
                                   .output() {
        if let Ok(owner) = String::from_utf8(py_output.stdout) {
            return Ok(owner);
        } else {
            return Err("Failed to convert url.py output to string");
        }
    } else {
        return Err("url.py invocation failed");
    }
}

fn get_ramp_up_score(owner: &str, repo: &str, token: &str) -> Result<f64, &'static str> {
    if let Ok(py_output) = Command::new("python3")
                                   .arg("src/url/ramp_up.py")
                                   .arg(owner)
                                   .arg(repo)
                                   .arg(token)
                                   .output() {
        if let Ok(ramp_up_score_str) = String::from_utf8(py_output.stdout) {
            if let Ok(ramp_up_score) = ramp_up_score_str.parse::<f64>() {
                return Ok(ramp_up_score);
            } else {
                return Err("Failed to convert ramp_up.py output to float");
            }
        } else {
            return Err("Failed to covert ramp_up.py output to string");
        }
    } else {
        return Err("ramp_up.py invocation failed");
    }
}

fn get_correctness_score(owner: &str, repo: &str, token: &str, rm_score: f64) -> Result<f64, &'static str> {
    if let Ok(py_output) = Command::new("python3") 
                                   .arg("src/url/correctness.py")
                                   .arg(owner)
                                   .arg(repo)
                                   .arg(token)
                                   .arg(rm_score.to_string())
                                   .output() {
        if let Ok(correctness_score_str) = String::from_utf8(py_output.stdout) {
            if let Ok(correctness_score) = correctness_score_str.parse::<f64>() {
                return Ok(correctness_score);
            } else {
                return Err("Failed to convert correctness.py output to float");
            }
        } else {
            return Err("Failed to covert correctness.py output to string");
        }
    } else {
        return Err("correctness.py invocation failed");
    }
}

fn get_bus_factor_score(owner: &str, repo: &str, token: &str) -> Result<f64, &'static str> {
    if let Ok(py_output) = Command::new("python3")
                                   .arg("src/url/bus_factor.py")
                                   .arg(owner)
                                   .arg(repo)
                                   .arg(token)
                                   .output() {
        if let Ok(bus_factor_score_str) = String::from_utf8(py_output.stdout) {
            if let Ok(bus_factor_score) = bus_factor_score_str.parse::<f64>() {
                return Ok(bus_factor_score);
            } else {
                return Err("Failed to convert bus_factor.py output to float");
            }
        } else {
            return Err("Failed to covert bus_factor.py output to string");
        }
    } else {
        return Err("bus_factor.py invocation failed");
    }
}

fn get_responsive_maintainer_score(owner: &str, repo: &str, token: &str) -> Result<f64, &'static str> {
    if let Ok(py_output) = Command::new("python3")
                                   .arg("src/url/responsive_maintainer.py")
                                   .arg(owner)
                                   .arg(repo)
                                   .arg(token)
                                   .output() {
        if let Ok(rm_score_str) = String::from_utf8(py_output.stdout) {
            if let Ok(rm_score) = rm_score_str.parse::<f64>() {
                return Ok(rm_score);
            } else {
                return Err("Failed to convert responsive_maintainer.py output to float");
            }
        } else {
            return Err("Failed to convert responsive_maintainer.py output to string");
        }
    } else {
        return Err("responsive_maintainer.py invocation failed");
    }
}

fn get_license_score(owner: &str, repo: &str, token: &str) -> Result<f64, &'static str> {
    if let Ok(py_output) = Command::new("python3")
                                   .arg("src/url/license.py")
                                   .arg(owner)
                                   .arg(repo)
                                   .arg(token)
                                   .output() {
        if let Ok(license_score_str) = String::from_utf8(py_output.stdout) {
            if let Ok(license_score) = license_score_str.parse::<f64>() {
                return Ok(license_score);
            } else {
                return Err("Failed to convert license.py output to float");
            }
        } else {
            return Err("Failed to covert license.py output to string");
        }
    } else {
        return Err("license.py invocation failed");
    }
}

fn net_score(mut ramp_up_score: f64,
             mut correctness_score: f64,
             mut bus_factor_score: f64,
             mut responsive_maintainer_score: f64,
             mut license_score: f64)
            -> f64 {
    //These lines deal with errors
    //if the scores return negative this will calculate the score with that subscore as 0
    if ramp_up_score < 0.0{
        ramp_up_score = 0.0
    }
    if correctness_score < 0.0{
        correctness_score = 0.0;
    }
    if bus_factor_score < 0.0{
        bus_factor_score = 0.0;
    }
    if responsive_maintainer_score < 0.0{
        responsive_maintainer_score = 0.0;
    }
    if license_score < 0.0{
        license_score = 0.0;
    }
    let net_score: f64 = 
        license_score * (
            0.3 * ramp_up_score +
            0.3 * correctness_score +
            0.1 * bus_factor_score +
            0.3 * responsive_maintainer_score
        );
    
    return net_score;
}

// Code adapted from "Rust By Example: 20.4.3"
// url: "https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html"
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>> where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[cfg(test)]
mod tests {
    static VALID_TEST_CASES: [(&str, &str, &str); 11] = [
        ("https://www.npmjs.com/package/even", "jonschlinkert", "even"),
        ("https://github.com/jonschlinkert/even", "jonschlinkert", "even"),
        ("https://github.com/SonarSource/chocolatey-packages", "SonarSource", "chocolatey-packages"),
        ("https://github.com/PSOPT/psopt", "PSOPT", "psopt"),
        ("https://github.com/nullivex/nodist", "nullivex", "nodist"),
        ("https://www.npmjs.com/package/express", "expressjs", "express"),
        ("https://www.npmjs.com/package/browserify", "browserify", "browserify"),
        ("https://github.com/cloudinary/cloudinary_npm", "cloudinary", "cloudinary_npm"),
        ("https://github.com/lodash/lodash", "lodash", "lodash"),
        ("https://github.com/PC192/ChubbyChecker", "PC192", "ChubbyChecker"),
        ("https://github.com/apache/airflow", "apache", "airflow")
    ];

    #[test]
    fn test_parse_url_file() {
        let url_file = "tests/test_cases.txt";

        match crate::parse_url_file(url_file) {
            Ok(urls) => {
                for i in 0..VALID_TEST_CASES.len() {
                    assert_eq!(VALID_TEST_CASES[i].0, urls[i]);
                }
            },
            Err(err) => eprintln!("{}", err)
        }
    }

    #[test]
    #[ignore = "not ready"]
    fn test_parse_url() {

    }

    #[test]
    #[ignore = "not ready"]
    fn test_get_package_scores() {

    }

    #[test]
    #[ignore = "not ready"]
    fn test_net_score() {

    }
}