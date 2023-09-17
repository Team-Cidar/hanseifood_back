pipeline {
    agent any

    stages {
        stage("Build") {
            steps {
                echo 'build docker image'
                sh 'docker compose build'
            }
            post {
                success {
                    echo '==========docker build succeed=========='
                }
                failure {
                    echo '==========docker build failed=========='
                }
            }
        }
        stage('Deploy'){
            steps {
                echo 'docker container start'
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
            post {
                success {
                    echo '==========docker deploy succeed=========='
                }
                failure {
                    echo '==========docker deploy failed=========='
                }
            }
        }
    }

    post {
        success {
            echo '==========Pipeline executed successfully=========='
        }
        failure {
            echo '==========Pipeline execution failed=========='
        }
    }
}