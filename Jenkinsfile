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
    stage('CLone Back') {
      parallel {
        stage('GIT PUSH') {
          steps {
            sh 'git clone -b develop https://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@github.com/fesflabs/diarias'
          }
        }
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/diarias_back/.env'
          }
        }
      }
    }
    stage('Para Containers') {
      steps{
        sh 'docker-compose down'
      }
    }
    stage('Cria repositório Front-end'){
      steps {
        sh 'mkdir diarias_front && cd diarias_front'
      }
    }
    stage('Push front') {
      parallel {
        stage('Clone Front ') {
          steps {
            sh 'git clone -b main https://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@github.com/fesflabs/diarias-front'
          }
        }
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/"Diarais prod"/diarias_front/diarias-front/.env'
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
        sh 'cd docker-compose up -d'
      }
    }

  }
}
