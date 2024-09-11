pipeline {
  agent {
    node {
      label 'diariadev'
    }

  }
  stages {     
    stage('Clone Back') {
      parallel {
        stage('GIT PUSH') {
          steps {
            sh 'git pull -b develop https://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@github.com/fesflabs/diarias'
          }
        }
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/diarias_dev/diarias/.env'
          }
        }
      }
    }
        stage('Acessa Back'){
      steps {
        sh 'cd /home/jenkins/workspace/diarias_dev/diarias && docker-compose down'
      }
    }   
    // stage('Para Containers') {
    //   steps{
    //     sh 'docker-compose down'
    //   }
    // }
    stage('Cria repositório Front-end'){
      steps {
        sh 'cd diarias_front'
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
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/diarias_dev/diarias-front/.env'
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
