// Resize a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize size infile outfile\n");
        return 1;
    }

    // remember filenames
    double size = atof(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // ensure size is 1 to 100
    if (size <= 0 || size > 100)
    {
        fprintf(stderr, "Please specify from 0.0 to 100.00 size only.\n");
        return 2;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, r_bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    r_bf = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, r_bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    r_bi = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // determine the new dimensions
    r_bi.biWidth = round(bi.biWidth * size);
    r_bi.biHeight = round(bi.biHeight * size);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int r_padding = (4 - (r_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // resize outfile's header
    r_bi.biSizeImage =
        ((sizeof(RGBTRIPLE) * r_bi.biWidth) + r_padding) * abs(r_bi.biHeight);
    r_bf.bfSize = r_bi.biSizeImage -
        sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // algothrim to reduce image size if less than 1
    int factor = 0;
    if (size < 1)
    {
        factor = round(100 / (size * 100));
        factor--;
        size = 1;
    }
    else factor = 0;

    // write outfile's BITMAPFILEHEADER
    fwrite(&r_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&r_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines and resize
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int j = 0; j < size; j++)
        {
            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // skip over n pixel to reduce image size
                for (int l = 0; l < factor; l++)
                    fseek(inptr, sizeof(RGBTRIPLE), SEEK_CUR);

                // resize the width
                for (int m = 1; m <= size; m++)
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
            // then add it back (to demonstrate how)
            for (int n = 0; n < r_padding; n++)
                fputc(0x00, outptr);

            // return to previous scanline
            if (j < size - 1)
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
        }
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // skip over n scanline to reduce image size
        for (int o = 0; o < factor; o++)
            fseek(inptr, bi.biWidth * sizeof(RGBTRIPLE) + padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
