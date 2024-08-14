function MatlabCompiler_lowResolutionAnalysis()
%% module 1: low resolution image analysis - demo for a single fish with/without cancer cells
uiwait(msgbox("Low resolution analysis: press OK to continue!"));
uiwait(msgbox("Please load data (tif and excel file), press OK to continue!"));

%set the path and filename
[fileList fileDir ] = uigetfile({'*.*'},'MultiSelect', 'on' );
% f = msgbox('Module 1 (low resolution analysis) is running ...')

%phase 1: load the Volumefish image and coordinate from excel file
% load the image3D
f = msgbox("Low resolution analysis is running. It will take a few minutes");

TiffPos = (strfind(fileList,'tif'));
TiffInd = find(~cellfun(@isempty,TiffPos));
image3D = load3DImage(fileDir, fileList{TiffInd});
XlsPos = (strfind(fileList,'xlsx'));
XlsInd = find(~cellfun(@isempty,XlsPos));
[NumData]=xlsread(fullfile(fileDir, fileList{XlsInd}));
%remove small components from image
[image3D] = remove_small_comp_image(image3D);
% extract coordinates of each cell in 3D from excel file
ScaleFactor = 1;% I downsample the image for segmentation (for paper ScaleFactor = 9.2)
X= NumData(:,25); % in pixel
Y= NumData(:,27);
Z= NumData(:,29);
% scale it properly
X= NumData(:,25)*ScaleFactor; % in pixel
Y= NumData(:,27)*ScaleFactor;
Z= NumData(:,29);

%phase 2: calculate the hopkins statistic through a boostrapping
dataXYZ = [X Y Z];
ParNum = size(X,1);
NTrial = 350; %number of trials for running Hopkins Stat
p_sampling = 0.1;   % between 0 to 1 meaning 30% of the datapoints considered for random position
nRand = round(p_sampling*ParNum); % number of random points
%generate random points within fish volume
close(f)

hWaitbar = waitbar(0, 'Hopkins statistic is running!') 
[RandIndex RandCoor_Total] = genRandomPixel3Dimage(image3D,nRand*NTrial);

%calculate the hopkins stat for NTrial times to find the confidence
%internval
for iTrial= 1: NTrial
    startInd = (iTrial-1)*nRand+1;
    endInd = iTrial*(nRand);
    RandCoor = RandCoor_Total(startInd:endInd,:);
    [clusterTend(iTrial,1)] = HopkinsStat(dataXYZ,RandCoor,nRand);
    waitbar(iTrial / NTrial, hWaitbar, sprintf('Processing... %d%%', round(iTrial/ NTrial * 100)));

end
delete(hWaitbar);

uiwait(msgbox('Low resolution analysis is complete, press OK to continue!',"Success","modal"));

s = sprintf('Cluster tendency is on average %.2f with standard deviation of %.2f. Press OK to continue!',mean(clusterTend), std(clusterTend));
uiwait(msgbox(s,"Success","modal"));

uiwait(msgbox('Hopkins statistic is saved in an excel file in data folder. Press OK and check the example folder.',"Success","modal"));

saveDirectory = [fileDir filesep 'Results'];
if ~isdir(saveDirectory) mkdir(saveDirectory); end
%save results
savename = 'lowResResults.xlsx';  % Example file name
writematrix(clusterTend, fullfile(saveDirectory,savename));

