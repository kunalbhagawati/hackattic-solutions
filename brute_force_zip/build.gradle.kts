group = "me.kunalbhagawati"
version = "1.0-SNAPSHOT"

plugins {
    id("java")
    kotlin("jvm") version "1.8.20"
    kotlin("plugin.serialization") version "1.8.20"
    id("org.jlleitschuh.gradle.ktlint") version "11.3.1"
}

repositories { mavenCentral() }

val fuelVersion: String = "2.3.1"

dependencies {
    implementation(kotlin("stdlib"))
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.5.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4")

    // Dotenv
    implementation("io.github.cdimascio:dotenv-kotlin:6.4.1")

    // Fuel ---
    // core
    implementation("com.github.kittinunf.fuel:fuel:$fuelVersion")
    // packages
    implementation("com.github.kittinunf.fuel:fuel-coroutines:$fuelVersion")
    implementation("com.github.kittinunf.fuel:fuel-kotlinx-serialization:$fuelVersion")
    // ---
}
