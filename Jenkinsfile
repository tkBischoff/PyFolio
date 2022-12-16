pipeline {
    agent any

    stages {
        stage("verify tooling") {
            steps {
                sh 'echo "################# verify tooling ###########################'
                sh '''
                    docker version
                    docker info
                    docker-compose version
                '''
            }
        }
        stage('SonarQube Analysis') {
            steps {
                sh 'echo "################# SonarQube Analysis ###########################'
                withSonarQubeEnv(installationName: 'sq1') {
                  sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage('Prune Docker Data'){
            steps{
                sh 'echo "################# Prune Docker Data ###########################'
                sh 'docker system prune -a --volumes'
            }
        }
        stage('Start container'){
            steps{
                sh 'echo "################# Start Container ###########################'
                sh 'docker-compose -f app/docker-compose.yaml up -d --wait'
                sh 'docker-compose -f app/docker-compose.yaml ps'
            }
        }
    }
    post {
        always{
            sh 'echo "################# cleanup ###########################'
            sh 'docker-compose -f app/docker-compose.yaml down --remove-orphans -v'
            sh 'docker-compose -f app/docker-compose.yaml ps'
        }
    }
}
