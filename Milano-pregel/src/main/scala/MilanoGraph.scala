import org.apache.log4j.{Level, Logger}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD


/*
Author : Charles GAYDON
03/12/2017
Master 2 Data Science
*/


object MilanoGraph {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Stats Graph").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val rootLogger = Logger.getRootLogger //import de org.apache.log4j
    rootLogger.setLevel(Level.ERROR) // pour éviter spark trop verbeux
    val file = "./src/main/ressources/MItoMI-2013-12-01-4Pregel.txt"
    val fileout = "./Results/MItoMI-2013-12-01-Pregelled.txt"
    case class Square(id: Int, value:Double)

    val Square_default = Square(0,1.toDouble) //one unit of information

    val nodes: RDD[(VertexId, Square)] =
      sc.parallelize(1 to 2)
        .map { id =>
          (id.toLong, Square(-1,-1.0.toDouble))
        }
    val links: RDD[Edge[Double]] =
      sc.textFile(file)
          //.filter(line => line(1)<5000 && line(1)>4600 && line(2)<5000 && line(2)>4600)
        .map { line =>
          val row = line split ','
          Edge(row(1).toLong, row(2).toLong, row(3).toDouble)
        }

    // we create a graoh and remove the oonstruction nodes.
    var g = Graph(nodes, links, Square_default)
    var G = g.subgraph(vpred = (id, attr) => attr.value!= -1.toDouble)
    G = G.mapVertices[Square]((id, attr) => Square(id.toInt, attr.value))
    //G.vertices.foreach(println)
    // A few info
    println("Total Number of Square: " + G.numVertices)
    println("Total Number of Communcation values: " + G.numEdges)
/*
    // A first iter with pagerank
    val ranks = G.pageRank(0.0001).vertices
    ranks
      .join(G.vertices)
      .sortBy(_._2._1, ascending=false) // sort by the rank
      .take(10) // get the top 10
      .foreach(x => println(x._2._2))
*/
    // Pregel this G
    val resetProb = 0.9
    def vertexProgram(id: VertexId, attr: Square, msgSum: Double): Square =
      Square(attr.id, (attr.value*resetProb + (1.0 - resetProb) * msgSum).toDouble)

    def sendMessage(ET: EdgeTriplet[Square, Double]) : Iterator[(VertexId, Double)] =
      Iterator((ET.dstId, ET.attr*ET.srcAttr.value)) //ici pribleme car trop bas.

    def messageCombiner(a: Double, b: Double): Double = (a + b) //essayer somme sinon
    val initialMessage = 0.0
    val numIter = 4
    // Execute Pregel for a fixed number of iterations.
    var G_pregel = Pregel(G, initialMessage, numIter, EdgeDirection.Either)(
      vertexProgram, sendMessage, messageCombiner)
    var masters = G_pregel.vertices.map(u => (u._2.id, u._2.value)).coalesce(1).sortBy(_._2, ascending=false)
    var tosave = masters
    tosave.foreach(u => println(u._1, u._2))
   // tosave.saveAsTextFile(fileout) //null string !

  }
}
