import React, { useState } from "react";
import Select from 'react-select';

import SinglePagePDFViewer from "./components/pdf/single-page";
import "./styles.css";

import data from './input.json';
import { useEffect } from "react";

var PdfList = [];
var options = [];
// let pdf_relative_path = "../public/pdf_docs/";
let pdf_relative_path = "./pdf_docs/";
for (let i = 0; i < data.topics.length; i++) {
    let samplePDF = require(pdf_relative_path + data.topics[i] + "/readme.pdf");
    PdfList.push(samplePDF);
    options.push({value: i, label: data.topics[i]});
}

var codes = [];
var codesName = [];
let code_relative_path = "../public/";
for (let i = 0; i < data.code_dir.length; i++) {
    codes.push([]);
    codesName.push([]);
    for (let j = 0; j < data.code_dir[i].length; j++) {
        codes[i].push(data.code_dir[i][j].replace(code_relative_path, ""));
        codesName[i].push(data.code_name[i][j]);
    }
}

export default function Pdf_renderer() {
    const [selectedOption, setSelectedOption] = useState(options[0]);
    const [idx, setIdx] = useState(0);

    function changePDFIdx(idx) {
        setIdx(idx);
    }

  return (
    <div className="App">
        <h1 id="ntu-header">National Taiwan University</h1>
        <h2 id="course-header">Time-Frequency Analysis & Wavelet Tranform (CommE5030) <br/>
            Adaptive Digital Signal Processing (EE5163) </h2>
        <h2 id='term-proj-header'>Term Project - Programming Implementations</h2>

        <div className="topic-selector">
            <h2>Term Project Topics:</h2>
            <Select 
            defaultValue={selectedOption}
            onChange={(e) => {
                setSelectedOption();
                changePDFIdx(e.value);
                }}
            options={options} />
        </div>
        
        <div id="readme-header"><h2>ReadMe</h2></div>
        <div className="pdf-container">
            <SinglePagePDFViewer pdf={PdfList[idx]} />
        </div>

        <div className='pdf-download-button'>
            <a href={PdfList[idx]} download>
                <div>Download PDF</div>
            </a>
        </div>

        <hr />
        
        <div className="programming-implementation">
            <h4>Programming Implementations:</h4>
            <ul>
                {
                    codes[idx].map((code, index) => (
                        <li>
                            <a className="code-download-link" href={code} download>
                                <div>{codesName[idx][index]}</div>
                            </a>
                        </li>
                    ))
                }
            </ul>
            
        </div>

    </div>
  );
}