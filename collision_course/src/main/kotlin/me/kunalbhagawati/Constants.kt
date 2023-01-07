package me.kunalbhagawati


object Constants {
    val HOST = "https://hackattic.com"
    val CHALLENGE_PATH = "challenges/{PROBLEM_NAME}"  // This is a pure string.
    val FETCH_PROBLEM_INPUTS_URL = "${HOST}/${CHALLENGE_PATH}/problem?access_token={ACCESS_TOKEN}"
    val SUBMIT_SOLUTION_URL = "${HOST}/${CHALLENGE_PATH}/solve?access_token={ACCESS_TOKEN}"
}
