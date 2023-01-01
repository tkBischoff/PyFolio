pipeline {
    agent any

    stages {
        stage("verify tooling") {
            steps {
                sh 'echo "################# verify tooling ###########################"'
                sh '''
                    docker version
                    docker info
                    docker-compose version
                '''
                script{
                    def scannerHome = tool 'sonar_scanner'
                    withSonarQubeEnv(installationName: 'sq1') {
                        sh "${scannerHome}/bin/sonar-scanner --version"
                    }
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                sh 'echo "################# SonarQube Analysis ###########################"'
                script{
                    def scannerHome = tool 'sonar_scanner'
                    withSonarQubeEnv(installationName: 'sq1') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage('Shutdown old Container'){
            steps{
                sh 'docker-compose -f app/docker-compose.yaml down --remove-orphans -v'
                sh 'docker-compose -f app/docker-compose.yaml ps'
            }
        }
        stage('Prune Docker Data'){
            steps{
                sh 'echo "################# Prune Docker Data ###########################"'
                sh 'docker system prune -a --volumes'
            }
        }
        stage('Deploy'){
            steps{
                sh 'echo "################# Deploying ###########################"'
                sh 'docker-compose -f app/docker-compose.yaml up -d'
                sh 'docker-compose -f app/docker-compose.yaml ps'
            }
        }
    }
}

