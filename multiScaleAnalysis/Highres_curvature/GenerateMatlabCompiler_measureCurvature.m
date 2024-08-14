function MatlabCompiler_measureCurvature()
%% module 3: measure curvature
uiwait(msgbox('Measuring curvature for a 3D cell shape. Press OK to continue!'));

%load data
[filename fileDir ] = uigetfile({'*.*'},'MultiSelect', 'on' );
f = msgbox("Measuring curvature is running. It will take a few minutes");

image3D = load3DImage(fileDir,filename);
surface = isosurface(image3D);


% smooth the triangle mesh
numIterations = 100; 
smoothMethod = 'Taubin'; %'Average', 'Laplacian','Taubin'
%redefine the mesh for having a proper input for smoothSurfaceMesh 
mesh = surfaceMesh(surface.vertices,surface.faces);
surfaceMeshOut = smoothSurfaceMesh(mesh,numIterations, "Method",smoothMethod);
surfaceSmooth.vertices = surfaceMeshOut.Vertices;
surfaceSmooth.faces = surfaceMeshOut.Faces;


% measure curvature using pricipal curvature
getderivatives = 0 
[PrincipalCurvatures,PrincipalDir1,PrincipalDir2,FaceCMatrix,VertexCMatrix,Cmagnitude]= GetCurvatures( surfaceSmooth ,getderivatives);
GaussianCurvatureUnsmoothed_vertex=PrincipalCurvatures(1,:).*PrincipalCurvatures(2,:);
meanCurvatureUnsmoothed_vertex=(PrincipalCurvatures(1,:)+PrincipalCurvatures(2,:))/2;

% convert curvature to physical value
pixelSize = 0.4; % projected pixelsize on camera in um
meanCurvatureUnsmoothed_vertex = meanCurvatureUnsmoothed_vertex/pixelSize; 

% remove high and low curvature for visualization purpose
meanCurvatureUnsmoothed_vertex (isnan(meanCurvatureUnsmoothed_vertex)) = nanmean(meanCurvatureUnsmoothed_vertex);
meanCurvatureUnsmoothed_vertex(meanCurvatureUnsmoothed_vertex<prctile(meanCurvatureUnsmoothed_vertex,1)) = prctile(meanCurvatureUnsmoothed_vertex,1); 
meanCurvatureUnsmoothed_vertex(meanCurvatureUnsmoothed_vertex< -1) = -1;
meanCurvatureUnsmoothed_vertex(meanCurvatureUnsmoothed_vertex > 1) = 1;

meanCurvatureUnsmoothed_vertex = meanCurvatureUnsmoothed_vertex';
GaussianCurvatureUnsmoothed_vertex = GaussianCurvatureUnsmoothed_vertex';
%save the results
saveDirectory = [fileDir filesep 'Results'];
if ~isdir(saveDirectory)
    mkdir(saveDirectory);
end
savename = 'Curvature.xlsx';  % Example file name
writematrix(meanCurvatureUnsmoothed_vertex, fullfile(saveDirectory,savename),'Sheet','meanCurvature_vertex');
writematrix(GaussianCurvatureUnsmoothed_vertex, fullfile(saveDirectory,savename),'Sheet','GaussianCurvature_vertex');
savename = 'meshSurface.xlsx';  % Example file name
writematrix(surface.vertices, fullfile(saveDirectory,savename),'Sheet','vertices');
writematrix(surface.faces, fullfile(saveDirectory,savename),'Sheet','faces');


% visualization, creating dae files for rendering in ChimeraX 
cmap = flipud(makeColormap('div_rwb', 1024));
climits = [-1 1];
daeSavePath=[saveDirectory filesep erase(filename,'.tif') '_curvature.dae'];
saveDAEfile(image3D, surfaceSmooth, meanCurvatureUnsmoothed_vertex, cmap, climits, daeSavePath);
close(f)
uiwait(msgbox('Curvature is saved in data folder. Press OK and check the example folder.',"Success","modal"));

