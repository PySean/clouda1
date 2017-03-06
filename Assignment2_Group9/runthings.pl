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
#Whack the output dir
print `bin/hadoop fs -rmr $outputdir`;
print `bin/hadoop jar hadoop-streaming-1.2.1.jar -D stream.map.output.field.separator=, -input /hw2-input -output $outputdir -mapper $mapper -reducer $reducer -file $mapper $reducer`;
