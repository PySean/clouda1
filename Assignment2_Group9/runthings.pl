#!/usr/bin/perl -w

if (@ARGV < 3) {
     #Input directory is fixed so only bother with the output one.
     print "Usage: ./runthings.pl outputdir mapper reducer\n";
     exit 1;
}
chomp @ARGV;
#Do the monkey with me!
$outputdir = shift @ARGV;
$mapper   = shift @ARGV;
$reducer  = shift @ARGV;
#Get prefix, remove trailing newline from echo output.
$hadoop_prefix = `echo \$HADOOP_PREFIX`;
chomp $hadoop_prefix;
#Whack the output dir
print `$hadoop_prefix/bin/hadoop fs -rmr $outputdir`;
print `$hadoop_prefix/bin/hadoop jar $hadoop_prefix/contrib/streaming/hadoop-streaming-1.2.1.jar -D map.output.field.separator=,  -file $mapper -mapper $mapper -file $reducer -reducer $reducer -input /hw2-input -output $outputdir`;
print `$hadoop_prefix/bin/hadoop fs -cat $outputdir/part-00000 > answer`;
