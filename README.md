# bennie

Bennie the Mandelbrodt Set

Fun story... or so...

After many years with LXC and Docker containers, I wanted to experiment with a
kubernetes cluster.  So I bought a set of 5 Fujitsu Futro 920, extended them to
16GB RAM and 256GB SSD, still waiting for the additional SATA cables to add 2TB
SSD drives to them.  Then I learned about k3s and am currently evaluating,
which distributed storage system I'll run as backing storage for my cluster.  I
set up a PXE install server to install bare metal automatically, installed
everything, and now I need something to scale out on my cluster before
migrating all my LXC containers and Podman pods to it.

And that's why we're here.  The Mandelbrodt set is completely easy to code (see
terminal.py) and it can be segmented into little chunks that can run in
parallel with many instances on my cluster.

Yeah, we're doing weird shit...

