
parentpath = "Z:/Fiolka/Manuscripts/2023-multiscale/rawdata/12791724/Exemplary_VisualizationDataset/low_resolutionsegmentation/";
segmentedfilename = "1_CH488_000000sg";

for (i = 0; i < 100; i++) {

close("*");

timepoint =  "t" + IJ.pad(i, 5);
currenttimepointpath = parentpath + File.separator + timepoint;
open(currenttimepointpath + File.separator + segmentedfilename + ".tif");
firstimage = getTitle();

//set lut and divide
run("Rainbow Smooth");
setMinAndMax(0, 500);
run("RGB Color");
run("Split Channels");

//save new windows
selectWindow(firstimage + " (red)");
saveAs("Tiff", currenttimepointpath + File.separator + segmentedfilename + "_red.tif");
selectWindow(firstimage + " (green)");
saveAs("Tiff", currenttimepointpath  + File.separator + segmentedfilename + "_green.tif");
selectWindow(firstimage + " (blue)");
saveAs("Tiff", currenttimepointpath + File.separator + segmentedfilename + "_blue.tif");

close("*");
}