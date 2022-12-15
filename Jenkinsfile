pipeline {
    agent any

    stages {
        stage("verify tooling") {
            steps {
                sh '''
                    docker version
                    docker info
                    docker-compose version
                '''
            }
        }
        stage('Prune Docker Data'){
            steps{
                sh 'docker system prune -a --volumes'
            }
        }
        stage('Start container'){
            steps{
                sh 'docker-compose -f app/docker-compose.yaml up -d --wait'
                sh 'docker-compose -f app/docker-compose.yaml ps'
            }
        }
    }
    post {
        always{
            sh 'docker-compose -f app/docker-compose.yaml down --remove-orphans -v'
            sh 'docker-compose -f app/docker-compose.yaml ps'
        }
    }
}
