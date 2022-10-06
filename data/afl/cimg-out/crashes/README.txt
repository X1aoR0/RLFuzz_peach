Command line used to find this crash:

./afl-fuzz -i /home/real/Rlfuzz-peach/rlfuzz/mods/Cimg-mod/SEED/ -o /home/real/Rlfuzz-peach/data/cimg-out -m none -t 1000+ /home/real/Rlfuzz-peach/rlfuzz/mods/Cimg-mod/image2ascii -i @@

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please drop
me a mail at <lcamtuf@coredump.cx> once the issues are fixed - I'd love to
add your finds to the gallery at:

  http://lcamtuf.coredump.cx/afl/

Thanks :-)
