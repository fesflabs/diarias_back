pipeline {
  agent {
    node {
      label 'diariadev'
    }

  }
  stages {
    stage('Cria repositorio back'){
      steps {
        sh 'mkdir diarias_back && cd diarias_back'
      }
    }        
    stage('Check Back') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias', branch: 'develop')
          }
        }
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/diarias_back/.env'
          }
        }
      }
    }
    stage('Cria repositório Front-end'){
      steps {
        sh 'mkdir diarias_front && cd diarias_front'
      }
    }
    stage('Check Front') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias-front', branch: 'main')
          }
        }
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/diarias_front/.env'
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
