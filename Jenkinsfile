pipeline {
  agent {
    node {
      label 'diariadev'
    }

  }
  stages { 
    stage ('Removendo repositorio'){
      steps{
        sh 'rm -rf diarias/'
      }
    } 
    //Clona back na branch Develop   
    stage('Clone Back') {
      parallel {
        stage('GIT PUSH') {
          steps {
            sh 'git clone -b develop https://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@github.com/fesflabs/diarias_back'
          }
        } //cria .env 
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/diarias_front_develop/diarias/.env'
          }
        }
      }
    } //Para containers rodando para evitar conflito de ID 
        stage('Acessa Back'){
      steps {
        sh 'cd /home/jenkins/workspace/diarias_front_develop/diarias && docker-compose down'
      }
    }   
    stage('Apagando front'){
      steps{
        sh 'rm -rf diarias-front'
      }
    }
    stage('Push front') { //clona front do repositório 
      parallel {
        stage('Clone Front ') {
          steps {
            sh 'git clone -b develop https://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@github.com/fesflabs/diarias-front'
          }
        } //cria .env front-end
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/env /home/jenkins/workspace/diarias_front_develop/diarias-front/.env'
          }
        }
      }
    }    //sanitiza maquinas
    stage('Limpando imagens e containers') {
      steps {
        sh 'docker system prune -a -f'
      }
    }

    stage('build') { //sobe containers
      steps {
        sh 'cd diarias && docker-compose up -d'
      }
    }
    stage('Listando Container'){
      steps{
        sh 'docker ps -a'
      }
    }

  }
}
