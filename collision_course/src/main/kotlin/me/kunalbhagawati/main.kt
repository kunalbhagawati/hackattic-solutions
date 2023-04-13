package me.kunalbhagawati

import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.serialization.responseObject
import com.github.kittinunf.result.Result
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.Serializable


@Serializable
data class HackatticData(
  val include: String
)

@Serializable
data class HackatticSolution(
  val files: List<String>
)

fun getData(): HackatticData {
  val (_, response, result) = Fuel
    .get(Constants.FETCH_PROBLEM_INPUTS_URL.replace(mapOf("ACCESS_TOKEN" to "91c1fcc096c67a9f")))
    .responseObject<HackatticData>()

  when (result) {
    is Result.Failure -> throw result.getException()
    is Result.Success -> return result.get()
  }
}

fun solve(data: HackatticData): HackatticSolution {
  runBlocking {
    launch {}
    launch {}
  }
}

//fun postSolution(solution: HackatticSolution): Unit = TODO()


fun main() {
  val data = getData()
  val solution = solve(data)
//  postSolution(solution)
}
