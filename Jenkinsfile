pipeline {
  agent {
    node {
      label 'diarias dev'
    }

  }
  stages {
    stage('CHECK') {
      steps {
        git(url: 'https://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@github.com/fesflabs/diarias', branch: 'main')
      }
    }

    stage('Deploy') {
      steps {
        sh 'docker-compose up -d'
      }
    }

  }
}