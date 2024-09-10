pipeline {
  agent {
    node {
      label 'diariadev'
    }

  }
  stages {        
    stage('CHECK') {
      parallel {
        stage('CHECK Back-end') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias', branch: 'develop')
          }
        }
    stage('CHECK Front-end') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias-front', branch: 'main')
          }
        }
                
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/.env'
          }
        }
    stage('Parando Containers') {
      steps {
        sh 'docker-compose down'
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
}
