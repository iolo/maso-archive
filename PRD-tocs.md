# TOC restoration

## INPUT
- new high quality cover images in `tocs` directory

## OUTPUT
- rename all files in `tocs` into `YYMM-NN.jpg`(NN might be page or sequence number for multi-page TOCs)
- OCR the TOC and compare with the existing TOC.md and update the TOC.md if there are any differences
- generate reduced(size/quality) images and apply to reading-room webapp.

## IMPORTANT NOTES
- Do **NOT** commit the donated high quality images
- Do **NOT** use the high quality images directly
  - because the donator may not want their high quality images to be used on afraid of copyright issues.
  - also, the high quality images are too large and will slow down the page load.

