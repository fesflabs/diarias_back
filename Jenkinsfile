pipeline {
  agent {
    node {
      label 'diariadev'
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
            sh 'cp /home/jenkins/var/env /home/jenkins/workspace/diarias_main/.env'
          }
        }

      }
    }

    stage('Limpando imagens e containers') {
      steps {
        sh 'docker system prune -a -f'
      }
    }

    stage('build') {
      steps {
        sh 'docker-compose up -d'
      }
    }

  }
}