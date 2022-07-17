# elmo_artefact

This repo holds the attempt of using ELMO to produce a "calibration artefact" defined in ISO 20085/2. Note that since the basis of ELMO is merely an instruction emulator---Thumbulator, I believe it is only sensible to "calibarate" the analysis part, but not the acquisition part. ELMO cannnot produce sensible simulation of the physical measurement anyway, so the purpose of this gadget is merely providing target traces for testing the power of side-channel analysis.

More details on ELMO can be found at https://github.com/sca-research/ELMO

## Leakage artefact
According to ISO 20085/2, a "calibration artefact" should produce leakage traces with a known security level---i.e. can be attacked within $N$ traces. If a side-cahnnel evaluation platform failed to find the secret key within $N$ traces, its security evaluation results can be questionable, as the tested attacks might not be ``optimal''. Although ELMO's leakage model misses a lot of realistic threat (see https://eprint.iacr.org/2021/756), if some platform already fails for an ELMO-based leakage artefact, it is highly unlikely it will survive more subtal realistic leakage models in practice. I believe the side-channel analysis module should be, to some extent, working relatively well for various existing leakage models: with today's CMOS technology, it becomes increasingly hard to ensure every single device share exactly the same leakage model. Assuming every single device follows the standard HW model is nothing more than a pure fantasy.

## Revision on ELMO
Technically speaking, ELMO can simulate *any* countermeasure that is completely written in Thumb instructions. The remaining issues are a) ELMO has no random noise and b) ELMO cannot simulate hardware-level random delay, e.g. non-cycle-wise random delay.

The former can be easily solved by adding a Guassian noise into ELMO's output. The entire trace will be added with the same 0-centerd noise with a certain variance. Although it is fairly common to use SNR here, as the signal power (variance) is hard to find, here we stay with noise variance.

The latter however, cannot be solved as ELMO only produces one point per cycle. However, there is one case we wish to add into ELMO: the random cycle-wise delay is often challenged by attackers trying to recover the randomness directly if the randomness is loaded into the microcontroller through some data-bus. If the CPU provids a random delay that can directly use the hardware randomness, without loading it through the data-bus. In practice, this usually means the leakage for randomness still exists, but much weaker than the counterpart on the data-bus. In ELMO, we simulate this by completely simualte random delay in ELMO simulation procedure, but not in ARM assembly. Therefore, the attackers see all delayed leakage, but not the randomness that controls the delay. Arguably, this is an optimistic case that is unlikely to exist in practice. However, this represents what the designer might be hoping for as stated in ISO 20085-2.


## Revision on workflow
We expect to modify the workflow of ELMO as follows:

- Each run of ELMO produces only 1 trace: although it is convenient to run $N$ traces within one call to ELMO; a drawback of this approach is all inputs, probably with some secret (e.g. unshared data, secret flag, etc.) running on the virtual ARM processor, which procudes leakage that is not seen in real life. Runing one trace per call simulates what the real device did, despite requires an additional script to connect/call ELMO.
- Acquisition script writes input through the txt file through "readbyte()", which is received by the ARM binary. It is recommended that for masked implementations, everything here should be protected. 
- Whenever fresh randomness is needed, please use "randbyte()" instead of C's rand(); otherwise it might leaks some info through executing rand()
- The output will be printed through "printbyte()": the acquisition script is responsible for reading back the output through the target txt

## Command line
> /elmo ${BINARY}.bin -noisestd 1 -randominterval 100 -randomdelay 5
- ${BINARY}.bin: ARM binary, for only 1 trace
- noisestd: standard deviation for gaussian noise
- randominterval: every xxx cycles, we will adding in some random delay (only for the triggered part)
- randomdelay: each time when some random delay is injected, how many cycles does the delay lasts
## Output data structure
> r=np.load("XXX.npz")
- r['input']: inputs for the procedure, usually plaintexts
- r['output']: outputs for the procedure, usually ciphertexts
- r['trace']: measured traces, 2D numpy array
- r['noisestd'],r['randominterval'],r['randomdelay']: parameters for the measurements


 
