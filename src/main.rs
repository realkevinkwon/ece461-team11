#![allow(non_snake_case)]

use std::{env, str, ffi::CStr, path::Path, fs::File, string::String};
use std::process::{exit, Command};
use std::io::{self, BufRead};
use lazy_static::lazy_static;
use regex::Regex;
use std::os::raw::{c_char, c_int};

const EXIT_SUCCESS: i32 = 0;
const EXIT_FAILURE: i32 = 1;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut outputs: Vec<String> = Vec::new();

    if Path::new(args[1].as_str()).exists() {
        let urls: Vec<String> = parse_url_file(args[1].as_str());
        let token = get_token();

        for url in urls.iter() {
            let (owner, repo): (String, String) = package(&url);

            let package_scores: Vec<f64> = package_scores(&owner, &repo, token.as_str());
            outputs.push(String::from(format!("{} {:.prec$} {:.prec$} {:.prec$} {:.prec$} {:.prec$} {:.prec$}",
                url,
                package_scores[5],
                package_scores[0],
                package_scores[1],
                package_scores[2],
                package_scores[3],
                package_scores[4],
                prec = 2,
            )));
        }

        for output in outputs.iter() {
            println!("{}", output);
        }
        exit(EXIT_SUCCESS);
    } else {
        println!("ERROR: File does not exist");
        exit(EXIT_FAILURE);
    }
}

fn package_scores(owner: &str, repo: &str, token: &str) -> Vec<f64> {
    let mut package_scores: Vec<f64> = Vec::new();

    let ramp_up_score: f64 = ramp_up_score(owner, repo, token);
    let correctness_score: f64 = correctness_score(owner, repo, token);
    let bus_factor_score: f64 = bus_factor_score(owner, repo, token);
    let responsive_maintainer_score: f64 = responsive_maintainer_score(owner, repo, token);
    // let license_score: f64 = license_score(owner, repo, token);

    package_scores.push(ramp_up_score);
    package_scores.push(correctness_score);
    package_scores.push(bus_factor_score);
    package_scores.push(responsive_maintainer_score);
    // package_scores.push(license_score);
    package_scores.push(net_score(
        ramp_up_score,
        correctness_score,
        bus_factor_score,
        responsive_maintainer_score,
        0.2
        // license_score
    ));

    return package_scores;
}

fn package(url: &str) -> (String, String) {
    let (owner, repo): (String, String) = parse_url(url);

    return (owner, repo);
}

fn parse_url(url: &str) -> (String, String) {
    // Determine source
    lazy_static! {
        static ref RE: Regex = Regex::new(
            r"\S*(github.com|npmjs.com)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-_.]+)"
        ).unwrap();
    }

    // &RE.captures(url).unwrap()

    let source = String::from(&RE.captures(url).unwrap()[1]);
    let mut owner = String::from(&RE.captures(url).unwrap()[2]);
    let repo = String::from(&RE.captures(url).unwrap()[3]);

    if source.eq("npmjs.com") {
        owner = npm_to_git(&repo);
    }

    return (owner, repo);
}

fn npm_to_git(repo: &str) -> String {
    let py_output = Command::new("python3")
                            .arg("src/url/url.py")
                            .arg(repo)
                            .output()
                            .expect("oops");

    let owner = String::from_utf8(py_output.stdout)
                       .unwrap();

    return owner;
}

fn parse_url_file(url_file: &str) -> Vec<String> {
    let mut urls: Vec<String> = Vec::new();

    // Read URLs from file
    if let Ok(lines) = read_lines(url_file) {
        for line in lines {
            if let Ok(url) = line {
                urls.push(url);
            }
        }
    }

    return urls;
}

fn get_token() -> String {
    let token = env::var("GITHUB_TOKEN").unwrap();

    return token;
}

// Code adapted from "PyO3 user guide: 7."
// url: "https://pyo3.rs/v0.18.0/python_from_rust.html"
fn ramp_up_score(owner: &str, repo: &str, token: &str) -> f64 {
    let py_output = Command::new("python3")
                         .arg("src/url/ramp_up.py")
                         .arg(owner)
                         .arg(repo)
                         .arg(token)
                         .output()
                         .expect("oops");

    let ramp_up_score = String::from_utf8(py_output.stdout)
                               .unwrap()
                               .parse::<f64>()
                               .unwrap();

    return ramp_up_score;
}

fn correctness_score(_owner: &str, _repo: &str, _token: &str) -> f64 {

    return 0.0;
}

fn bus_factor_score(_owner: &str, _repo: &str, _token: &str) -> f64 {

    return 0.0;
}

fn responsive_maintainer_score(owner: &str, repo: &str, token: &str) -> f64 {
    let py_output = Command::new("python3")
                         .arg("src/url/responsive_maintainer.py")
                         .arg(owner)
                         .arg(repo)
                         .arg(token)
                         .output()
                         .expect("oops");

    let responsive_maintainer_score = String::from_utf8(py_output.stdout)
                                             .unwrap()
                                             .parse::<f64>()
                                             .unwrap();

    return responsive_maintainer_score;
}

// fn license_score(_owner: &str, _repo: &str, _token: &str) -> f64 {

//     return 0.0;
// }

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

#[no_mangle]
pub extern "C" fn license_score(license: *const c_char, license_list: *const c_char) -> i32{
    // Using Unsafe to dereference the pointer and converting it to bytes
    let c_ptr_to_bytes = unsafe { CStr::from_ptr(license).to_bytes() };

    // Using Unsafe to dereference the pointer and converting it to bytes
    let c_ptr_to_bytes2 = unsafe { CStr::from_ptr(license_list).to_bytes() };

    // Converting from bytes to a string
    let license = str::from_utf8(c_ptr_to_bytes).unwrap();

    // Converting from bytes to a string
    let license_list = str::from_utf8(c_ptr_to_bytes2).unwrap();

    // Unwrap, in case license is empty or null
    // Return 1 if GNU v2.1 License found
    if license_list.contains(license) {
        return 1;
    }
    else{
        return 0;
    }
}

//  #[no_mangle]
//  pub extern "C" fn get_rm_score(rm_score: c_int) -> c_int{
//     let correctness_rm_score = 3;
//     let score = rm_score * correctness_rm_score;
//     return score;
//  }

// Returns 0 and should return score
// use std::ffi::CStr;
// use std::os::raw::c_char;
// use std::os::raw::c_int;
// use std::str;

// #[no_mangle]
// pub extern "C" fn bus_score(val: i32)-> i32{
// //     // let URL: &str = "https://github.com/Chise7/ECE461_Team11";
// //     // let repo = Repository::open(URL).expect("Couldn't create file");

// //     // let mut revwalk = repo.revwalk().expect("None");
// //     // revwalk.push_head();
// //     // let mut authors: Vec<String> = revwalk.map(|r| {
// //     //     let oid = r;
// //     //     repo.find_commit(oid)
// //     // })

//     let mut result:i32 = 0; 
//     if val >= 5 && val < 100{
//         result = 75;
//     } 
//     if val >= 100 {
//         result = 100;
//     };
//     return result
// }


// pub extern "C" fn net_score(bus:i32, correct:i32, responsive:i32, ramp:i32, license:i32)->i32{
//     let result:i32 = (((10 * bus)+(30*responsive)+(30*correct) + (30*ramp))*license) / 100;
//     return result
// }

// // Returns 0 and should return score
// #[macro_use]
// extern crate cpython;

// use cpython::{PyResult,Python};

// py_module_initializer!(mylib, |py, m| {
//     // m.add(py, "__doc__", "This module is implemented in Rust.")?;
//     m.add(py, "get_result", py_fn!(py, get_result(val: &str)))?;
//     Ok(())
// });

// fn get_result(_py: Python, val: &str) -> PyResult<String> {
//     Ok("Rust says: ".to_owned() + val)
// }