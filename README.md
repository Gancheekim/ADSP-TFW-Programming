# ADSP/TFW Term-project Programming Implementation Display website

## Guidance
1. install JavaScript and Yarn 
    - Yarn installation guide: https://www.hostinger.com/tutorials/how-to-install-yarn
2. In terminal, cd to root directory, type ```yarn``` to install all the package
3. ```yarn start``` to check if the website functions normally. Please check your browswer at ```localhost:3000```
4. add any new term-project: [Add new term-project](#Add-new-term-project)
5. ```yarn build``` to bundle up and re-compile all of the source code and docs, which will appear at ```build/``` directory
6. move the ```build``` directory to anywhere desired
7. points the website to ```build/index.html```


## Add new term-project
1. add description pdf
    - ```cd src/pdf_docs/```
    - ```mkdir <term-project-name>```
    - move the pdf into ```<term-project-name>``` and rename it into ```readme.pdf```
2. add any source codes 
    - ```cd public/docs/```
    - ```mkdir <term-project-name>```, the ```<term-project-name>``` must be same as above
    - move all the files into the directory.
3. after all the term-projects are added, please execute:
    - ```cd src/```
    - ```node read_docs.js```
    - changes will be recorded in ```input.json```, which is used to re-compile the website's static html
