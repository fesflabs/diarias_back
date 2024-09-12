pipeline {
  agent {
    node {
      label 'diariadev'
    }
//Apaga repositório anterior do back 
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
            sh 'git clone -b develop https://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@github.com/fesflabs/diarias'
          }
        } //cria .env 
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/envback /home/jenkins/workspace/diarias_dev/diarias/.env'
          }
        }
      }
    } //Para containers rodando para evitar conflito de ID 
        stage('Acessa Back'){
      steps {
        sh 'cd /home/jenkins/workspace/diarias_dev/diarias && docker-compose down'
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
            sh 'git clone -b main https://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@github.com/fesflabs/diarias-front'
          }
        } //cria .env front-end
        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/variaveis/diarias/envfront /home/jenkins/workspace/diarias_dev/diarias-front/.env'
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
