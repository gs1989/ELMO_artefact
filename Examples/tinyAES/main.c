
#include "aes.h"

#include <stdio.h>
#include <stdlib.h>
#include "elmoasmfunctionsdef.h"



int main( ) {


     uint8_t *input, *output;
    uint32_t i,j;
    uint32_t N;
    struct AES_ctx ctx;
    static const uint8_t key[16] = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};
    input = malloc(16*sizeof(uint8_t));

    AES_init_ctx(&ctx, key);

    for(j=0;j<16;j++)
    	readbyte(input+j); // Read plaintext
  
    //Encryption
    starttrigger();
    AES_ECB_encrypt(&ctx, input);   
    endtrigger();
    for(j=0;j<16;j++)
    	printbyte(input+j); // Write ciphertext
    endprogram();
  
    return 0;
}
