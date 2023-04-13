package me.kunalbhagawati

import com.github.kittinunf.fuel.Fuel
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking


data class HackatticData(
    val include: String
)

typealias HackatticSolution = Pair<String, String>

fun getData(): HackatticData {
    Fuel.get(Constants.FETCH_PROBLEM_INPUTS_URL)
}

fun solve(data: HackatticData): HackatticSolution {
    runBlocking {
        launch {}
        launch {}
    }
    TODO()
}

fun postSolution(solution: HackatticSolution): Unit = TODO()


fun main() {
    val data = getData()
    val solution = solve(data)
    postSolution(solution)
}
