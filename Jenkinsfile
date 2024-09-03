pipeline {
  agent {
    node {
      label 'diarias dev'
    }

  }
  stages {
    stage('CHECK') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias', branch: 'main')
          }
        }

        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/.env /home/jenkins/workspace/diarias_main'
          }
        }

      }
    }

    stage('Deploy') {
      steps {
        sh 'docker-compose up -d'
      }
    }

  }
}