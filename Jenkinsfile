pipeline {
  agent {
    node {
      label 'diariadev'
    }

  }
  stages {        
    stage('Parando Containers') {
      steps {
        sh 'cd /home/jenkins/variaveis/diarias && docker-compose down -d'
      }
    }
    stage('CHECK') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias', branch: 'develop')
          }
        }

        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/.env'
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
