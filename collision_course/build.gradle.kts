group = "me.kunalbhagawati"
version = "1.0-SNAPSHOT"


plugins {
    id("java")
    kotlin("jvm") version "1.8.0"
    kotlin("plugin.serialization") version "1.8.0"
}

repositories {
    mavenCentral()
}

val fuelVersion: String = "2.3.1"

dependencies {
    implementation(kotlin("stdlib"))
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.4.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4")

    // Fuel ---
    //core
    implementation("com.github.kittinunf.fuel:fuel:$fuelVersion")
    //packages
    implementation("com.github.kittinunf.fuel:fuel-coroutines:$fuelVersion")
    implementation("com.github.kittinunf.fuel:fuel-kotlinx-serialization:$fuelVersion")
    // ---
}
