pipeline {
  agent {
    node {
      label 'diariaprod'
    }

  }
  stages {
    stage('Parando Containers'){
      steps{
        sh 'cd /home/jenkins/var && docker-compose down'
      }
    }
    stage('CHECK') {
      parallel {
        stage('CHECK') {
          steps {
            git(url: 'https://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@github.com/fesflabs/diarias', branch: 'main')
          }
        }

        stage('criar .env') {
          steps {
            sh 'cp /home/jenkins/var/env /home/jenkins/workspace/diarias_producao/.env'
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
