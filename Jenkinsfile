pipeline {
    agent any
    parameters {
        string description: 'Tag to be executed by pytest, please set like this e.g. "-t @sanity"', name: 'Tag'
        }
    stages {
        stage('python version') {
            steps {
              sh 'python3 --version'
            }
        }
        stage('Run Python Scripts') {
            steps {
                withPythonEnv('python3') {
                    sh "echo ${params.Tag}"
                    sh 'pip install -r requirements.txt'
                    sh "python3 -m behave ${params.Tag}"
                }
                
            }
        }
        stage('reports') {
            steps {
                script {
                    allure ([
                        includeProperties: false,
                        jdk:'',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure']]
                    ])
                 }
            }
        }
    }
}