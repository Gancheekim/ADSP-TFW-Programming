var glob = require("glob-all");

const docsStorageDir = '../public/docs';

let files = glob.sync([docsStorageDir + '/**']);

let termTopics = []
let codes = [];
let codesName = [];
function cleanData(dirName) {
    if ((dirName != docsStorageDir) && (!dirName.replace("..", "").includes('.')) && (!dirName.includes("Makefile"))) {
        termTopics.push(dirName.replace(docsStorageDir + '/', ''));
        codes.push([]);
        codesName.push([])
    }
    else if ((!dirName.includes('.pdf')) && (dirName != docsStorageDir)) {
        console.log(dirName);
        codes[codes.length-1].push(dirName);
        codesName[codesName.length-1].push(dirName.split("/").slice(-1)[0]);
    }
}

files.forEach(cleanData);

const data = {
    "topics": termTopics,
    "code_dir": codes,
    "code_name": codesName
}


var fs = require('fs');
fs.writeFile ("input.json", JSON.stringify(data, null, 4), function(err) {
    if (err) throw err;
    console.log('complete');
    }
);