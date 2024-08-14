function MatlabCompiler_highResolutionAnalysis()

%% module 2: high resolution image analysis for two timepoints are needed as we will do the boostrapping
uiwait(msgbox('High resolution analysis: press OK to continue!'));
uiwait(msgbox("Please indicate path to data folder containing timepoints, press OK to continue!"));

%get the fileDirectory for cell ideas
[fileDir ] = uigetdir();
hWaitbar = waitbar(0, 'Calculating global geometrical features'); 

%save the folder information in this directory
timefolderList = dir(fileDir);
numTimes = size(timefolderList,1) - 2; % the first two structures are hidden folders

% loop over time
for iTime = 1: numTimes
    timeID = iTime + 2;
    folderTimeDir = [fileDir filesep timefolderList(timeID).name ];
    folderListCell = dir(folderTimeDir);
    numCells = size(folderListCell,1) - 2; % the first two structures are hidden folders

    imagename = 'segmentedImage.tif';

    % phase 1: calculate the global geometrical features for one time point
    for iCell = 1: numCells
        %phase 1: load the segmented cell
        fileID = iCell +2; %the first two folders are hidden
        cellPath = [folderTimeDir filesep folderListCell(fileID).name];
        image3D = load3DImage(cellPath, imagename);

        %phase 2: calculate the global features
        saveCellPath=[cellPath filesep 'GlobalMorphology'];
        if ~isfolder(saveCellPath)
            mkdir(saveCellPath);
        end
        %caculate the global feature for 3D image
        [globalGeoFeature convexImage Image] = calGlobalGeometricFeature(image3D);

        %save the global feature for each cell
        save(fullfile(saveCellPath,'globalGeoFeature.mat'),'globalGeoFeature');
        save(fullfile(saveCellPath,'convexImage.mat'),'convexImage');
        save(fullfile(saveCellPath,'Image.mat'),'Image');
    end
waitbar(iTime / numTimes, hWaitbar, sprintf('Calculating global geometrical features... %d%%', round(iTime/ numTimes * 100)));

end
delete(hWaitbar);

hWaitbar = waitbar(0, 'Calculating pca...');

%phase 3: calculate the pc space
featType=[ {'Volume'} {'SurfaceArea'} ...
    {'Sphericity'} {'Solidity'} {'LongLength'} {'AspectRatio'}...
    {'Roughness'} {'Extent'} {'CirmuscribedSurfaceRatio'} ...
    {'VolumeSphericity'} {'RadiusSphericity'} {'RatioSphericity'}];

GeoFeaturesTable = [];
%initialize geometric feature table
for iTime = 1:numTimes
    timeID = iTime + 2;
    folderTimeDir = [fileDir filesep timefolderList(timeID).name ];

    %check the number of cell in each timepoint folder
    dirInfo = dir(folderTimeDir);
    dirInfoName = extractfield(dirInfo,'name');
    fileList = dirInfoName(3:end)'; % exclude '.' and '..' from the list
    cellList = str2double(erase(fileList, 'Cell'));
    cellList = sort(cellList);

    GeoFeaturesTabletmp=createGeoFeaturesTable(folderTimeDir,cellList,featType);

    % add timepoint as an experimental condition
    GeoFeaturesTabletmp.ExpCondition(:) = {timefolderList(timeID).name};

    GeoFeaturesTable = [GeoFeaturesTable; GeoFeaturesTabletmp];
    waitbar(iTime / numTimes, hWaitbar, sprintf('Calculating pca... %d%%', round(iTime/ numTimes * 100)));

end


[statMat statMat_Norm]=createStatMatrix(GeoFeaturesTable,featType);

% PCA
plotFlag=1;
[coeff,pcCoor,eigenValues,tsquared,Contribution,mu]=calPCA_globalGeometry(statMat_Norm,plotFlag,featType);
delete(hWaitbar);

%phase 4: measure the pvalue through boostrapping, metric = 'Tukey'
hWaitbar = waitbar(0, 'Calculating pvalue...'); 

N_dim = 2; % calculate the pvalue for N_dim of pc space

%boosttrapping parameters for pvalue
Ntrials=300;  % number of iteration
metric='TukeyMedian';  % other matric: ConvexHull , mean ,TukeyMedian
genSample='randomLabel'; %method to sample the point for boostrapping

%initialize the pvalue matrix
Pvalue_matrix = ones(numTimes);
for iTime = 1: numTimes
    % find index of dist 1
    Ind1 = find(statMat(:,end) == iTime);
    dist1 = pcCoor(Ind1,1:N_dim);
    %loop over dist 2
    for iTime2 = 1:numTimes
        if iTime2 ==iTime
            continue
        end 
        Ind2 = find(statMat(:,end) ==iTime2);
        dist2 = pcCoor(Ind2,1:N_dim);
    
    [pValue compDist comp2Dists] =bootstrapping2DistComp(dist1,dist2,Ntrials,metric,genSample);
    %iTime starts from 0
    Pvalue_matrix(iTime,iTime2) = pValue;
iTime2
    end
    
    waitbar(iTime / numTimes, hWaitbar, sprintf('Calculating pvalue... %d%%', round(iTime/ numTimes * 100)));

end 
delete(hWaitbar);

%save results
figure; 
heatmap(Pvalue_matrix);
title('Pvalue of Geometrical Features in PC Space');
xlabel('Time index');
ylabel('Time index');
uiwait(msgbox('High resolution analysis is complete, press OK to continue!',"Success","modal"));

saveDirectory = [fileDir filesep 'Results'];
if ~isdir(saveDirectory)
    mkdir(saveDirectory);
end

savename = 'PvalueMatrix.png';
saveas(gcf, fullfile(saveDirectory,savename));

savename = 'FeatureSpace_pcSpace.png';
saveas(figure(1), fullfile(saveDirectory,savename));

savename = 'data_pcSpace.png';
saveas(figure(2), fullfile(saveDirectory,savename));

savename = 'PC_contribution.png';
saveas(figure(3), fullfile(saveDirectory,savename));

close all
%save results
savename = 'highResResults_pca.xlsx';  % Example file name
pcCoorT = array2table(pcCoor);
writetable(pcCoorT, fullfile(saveDirectory,savename),'Sheet','PCCoordinate');
writematrix(Contribution, fullfile(saveDirectory,savename),'Sheet','PCContribution');

savename = 'highResResults_geoTable.xlsx';  % Example file name
writetable(GeoFeaturesTable, fullfile(saveDirectory,savename),'Sheet','GlobalShapeFeatures');

savename = 'highResResults_pvalue.xlsx';  % Example file name
Pvalue_matrixT = array2table(Pvalue_matrix);
writetable(Pvalue_matrixT, fullfile(saveDirectory,savename),'Sheet','PvalueMatrix');

uiwait(msgbox('Global geometrical feature table and figures are saved in data folder. Press OK and check the example folder.',"Success","modal"));


