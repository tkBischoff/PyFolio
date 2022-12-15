pipeline {
    agent any
    stage('Initialize'){
        def dockerHome = tool 'DockerInstall'
        env.PATH = "${dockerHome}/bin:${env.PATH}"
    }

    stages {
        stage("verify tooling") {
            steps {
                sh '''
                    docker version
                    docker info
                    docker compose version
                    curl --version
                    jq --version
                '''
            }
        }
    }
}
