pipeline {
  agent {
    node {
      label 'agente diarias'
    }

  }
  stages {
    stage('CHECK') {
      steps {
        git(url: 'https://github.com/fesflabs/diarias', branch: 'main')
      }
    }

    stage('Deploy') {
      steps {
        sh 'docker-compose up -d'
      }
    }

  }
}