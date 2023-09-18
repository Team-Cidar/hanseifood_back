pipeline {
    agent any

    environment {
        DB_NAME="mysql_service"
        WAS_NAME="hanseifood_was"
    }
    stages {
        stage("Build") {
            steps {
                echo '==========build docker image=========='
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
        stage("Stop and remove existing container") {
            steps {
                echo '==========stop and remove container=========='
                sh 'docker compose stop'
                sh 'docker rm -f ${DB_NAME} ${WAS_NAME}'
            }
            post {
                success {
                    echo '==========stop & remove succeed=========='
                }
                failure {
                    echo '==========stop & remove failed=========='
                }
            }
        }
        stage('Deploy'){
            steps {
                echo '==========docker container start=========='
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