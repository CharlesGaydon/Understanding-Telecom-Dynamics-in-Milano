name := "Milano-pregel"

version := "0.1"

scalaVersion := "2.11.8"


libraryDependencies += "org.apache.hadoop" % "hadoop-client" % "2.7.3"
libraryDependencies += "org.apache.spark" %% "spark-core" % "2.2.0"
libraryDependencies += "org.apache.spark" %% "spark-mllib" % "2.2.0"
assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}