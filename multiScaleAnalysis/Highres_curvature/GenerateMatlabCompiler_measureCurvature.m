function MatlabCompiler_measureCurvature()
%% module 3: measure curvature
uiwait(msgbox('Measuring curvature for a 3D cell shape. Press OK to continue!'));
uiwait(msgbox("Please load data (tif file), press OK to continue!"));

%load data
[filename fileDir ] = uigetfile({'*.*'},'MultiSelect', 'on' );

hWaitbar = waitbar(0, 'Measuring curvature is running...'); 
nStep = 3; 
iStep = 1; 
waitbar(iStep / nStep, hWaitbar, sprintf('Loading data ... %d%%', round(iStep/ nStep * 100)));

image3D = load3DImage(fileDir,filename);

%check if it is a binary image
imageValue = unique(image3D(:)); 
if numel(imageValue) > 3
    warning('No binary image was provided. A binary image will be automatically created, please verify the results or provide a binary image.')
   
    %normalize the image3D first 
    image3D = imadjustn(image3D);
    % use easy threshold to make a binary object
    thresh = multithresh(image3D);
    image3D (image3D <thresh) = 0;
    image3D (image3D >= thresh) = 1;

    se = strel('sphere',10);

    image3D = imclose(image3D,se);
    image3D = imfill(image3D);

    CC = bwconncomp(image3D);
    CClength = cellfun(@length, CC.PixelIdxList);
    [  MaxCC MaxCCInd] = max(CClength);
    image3D = zeros(size(image3D));
    image3D(CC.PixelIdxList{MaxCCInd}) = 1;
    image3D = single(image3D);

    % smoothe the binary image 
    % sigma = 1; 
    % [image3D] = filterGauss3D(image3D, sigma);
    %or using the smooth3 function in MATLAB
    image3D = smooth3(image3D); 
end

iStep = 2; 
waitbar(iStep / nStep, hWaitbar, sprintf('Generating a triangle mesh ... %d%%', round(iStep/ nStep * 100)));

%make a surface
surface = isosurface(image3D);

% smooth the triangle mesh using MATLAB function but it needs version 2023a
% (method 1)
% alternative is from this github repository (method 2)
% (https://github.com/alecjacobson/gptoolbox)
if numel(imageValue) < 3 % binary input
    %smoothing the mesh - method 1
    numIterations = 100;
    smoothMethod = 'Taubin'; %'Average', 'Laplacian','Taubin'
    %redefine the mesh for having a proper input for smoothSurfaceMesh
    mesh = surfaceMesh(surface.vertices,surface.faces);
    surfaceMeshOut = smoothSurfaceMesh(mesh,numIterations, "Method",smoothMethod);
    surfaceSmooth.vertices = surfaceMeshOut.Vertices;
    surfaceSmooth.faces = double(surfaceMeshOut.Faces);
    surface = surfaceSmooth;
    warning('Check if the mesh is smooth before running the curvature.')
end

%smoothing the mesh - method 2
% L_method = 'cotan'; 
% method = 'implicit';    
% lambda = 0.001; %default is too smooth
% [surface.vertices] = laplacian_smooth(surface.vertices,surface.faces,L_method,[],lambda,method,surface.vertices,numIterations);
% method 3: recommended (fast) and better for non-binary image3D
if numel(imageValue) > 3 %for non-binary input
    delta = 1e-5; % one is to turn it to a sphere, maxIter isn't so effective
    [surface.vertices] = conformalized_mean_curvature_flow(surface.vertices,surface.faces,'delta', delta, 'RescaleOutput', true);
end
iStep = 3; 
waitbar(iStep / nStep, hWaitbar, sprintf('Measruing curvature ... %d%%', round(iStep/ nStep * 100)));

% measure curvature using pricipal curvature method 1, 
%measure curvature using gpttoolbox, method 2
getderivatives = 0 ;
[PrincipalCurvatures,PrincipalDir1,PrincipalDir2,FaceCMatrix,VertexCMatrix,Cmagnitude] = GetCurvatures( surface ,getderivatives);
GaussianCurvatureunSmoothed_vertex = real(PrincipalCurvatures(1,:).*PrincipalCurvatures(2,:));
meanCurvatureunSmoothed_vertex = real((PrincipalCurvatures(1,:)+PrincipalCurvatures(2,:))/2);

% % method 2 
% [k,meanCurvatureunSmoothed_vertex,GaussianCurvatureunSmoothed_vertex,M,T] = discrete_curvatures(surface.vertices,surface.faces);

% convert curvature to physical value
pixelSize = 0.4; % projected pixelsize on camera in um for multiscale
meanCurvatureunSmoothed_vertex = meanCurvatureunSmoothed_vertex/pixelSize; 

% remove high and low curvature for visualization purpose
meanCurvatureunSmoothed_vertex (isnan(meanCurvatureunSmoothed_vertex)) = nanmean(meanCurvatureunSmoothed_vertex);
meanCurvatureunSmoothed_vertex(meanCurvatureunSmoothed_vertex<prctile(meanCurvatureunSmoothed_vertex,1)) = prctile(meanCurvatureunSmoothed_vertex,1); 
meanCurvatureunSmoothed_vertex(meanCurvatureunSmoothed_vertex< -1) = -1;
meanCurvatureunSmoothed_vertex(meanCurvatureunSmoothed_vertex > 1) = 1;

meanCurvatureunSmoothed_vertex = meanCurvatureunSmoothed_vertex';
GaussianCurvatureunSmoothed_vertex = GaussianCurvatureunSmoothed_vertex';

%save the results
saveDirectory = [fileDir filesep 'Results'];
if ~isdir(saveDirectory)
    mkdir(saveDirectory);
end

savename = 'Curvature.xlsx';  % Example file name
writematrix(meanCurvatureunSmoothed_vertex, fullfile(saveDirectory,savename),'Sheet','meanCurvature_vertex');
writematrix(GaussianCurvatureunSmoothed_vertex, fullfile(saveDirectory,savename),'Sheet','GaussianCurvature_vertex');
savename = 'meshSurface.xlsx';  % Example file name
writematrix(surface.vertices, fullfile(saveDirectory,savename),'Sheet','vertices');
writematrix(surface.faces, fullfile(saveDirectory,savename),'Sheet','faces');

% visualization, creating dae files for rendering in ChimeraX 
cmap = flipud(makeColormap('div_rwb', 1024));
climits = [-1 1];
daeSavePath=[saveDirectory filesep erase(filename,'.tif') '_curvature.dae'];
saveDAEfile(image3D, surface, meanCurvatureunSmoothed_vertex, cmap, climits, daeSavePath);
delete(hWaitbar);

uiwait(msgbox('Curvature is saved in data folder. Press OK and check the example folder.',"Success","modal"));

