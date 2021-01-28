const input = document.getElementById('faceShotSelector');
const inputDouble = document.getElementById('faceShotSelectorDouble');

input.addEventListener('change', updateInputDouble);

function updateInputDouble() {
    if (input.files.length === 0) {
        inputDouble.innerHTML = "Please select a JPG/JPEG file...";
        return
    }

    const curFile = input.files[0];

    if (!isJPEG(curFile)) {
        inputDouble.innerHTML = "Not a valid JPG/JPEG!";
        clearFileList(input);
        return
    }

    inputDouble.innerHTML = curFile.name;
}

function isJPEG(fileObj) {
    return fileObj && /\.(jpe?g)$/i.test(fileObj.name) && /image\/*/.test(fileObj.type)
}

function clearFileList(inputElement) {
    let _mockElt = document.createElement('input');
    _mockElt.type = 'file';
    inputElement.files = _mockElt.files;
}
