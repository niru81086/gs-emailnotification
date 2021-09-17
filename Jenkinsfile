#!/usr/bin/env groovy   
@Library('myshared-library')_

 pipeline {
// define global agent
    agent {label 'master'}

 
// define environment variable 
        environment {
            scannerHome = tool 'sonar4.6'
            imageName = "email-notification"
            qa= 'qa'
            stage= 'stage'
            dev= 'dev-'
            blank= ''
            registryCredentials = "Nexus"
            registry = "192.168.0.5:8050"
            dockerStageImage = ''
            dockerQAImage = ''
            versionTags= versiontags()
            Tags= '$BUILD_NUMBER'
            
        }
            // This stage perform flake8 analysis when there is any new commit on dev branch          
    stages {
        stage('Dev-StaticCodeAnalysis') {
            when {
                branch 'dev'
                beforeAgent true
            }
            agent {label 'slave'}
            steps {
                   sh '''#!/bin/bash 
                   docker rm -f flake8
                   CONTAINER_python=$(docker run -d -t -e PYTHONUNBUFFERED=0 -w /root -v $WORKSPACE:/root  --name flake8 python:3.7-alpine /bin/sh)
                   docker exec -i $CONTAINER_python /bin/sh  -c "pip install flake8 && flake8 --exit-zero --format=pylint  RabbitMQ_Consumer/ >flake8-out.txt"
                       #python3.7 -m virtualenv my-venv 
                        #source  my-venv/bin/activate
                        #ip install flake8
                        #flake8 --format=pylint  RabbitMQ_Consumer/ >flake8-out.txt
                        #deactivate
                        
                   '''    
                }
        }
                // This stage perform UiteTest when there is any new commit on dev branch
        stage('Dev-UnitTest') {
            when {
                branch 'dev'
                beforeAgent true
            }
            agent {label 'slave'}
            options { skipDefaultCheckout() }
            steps {
                /*
                 sh '''#!/bin/bash -x
                        python3.7 -m virtualenv my-venv 
                        source  my-venv/bin/activate
                        pip install -r requirements.txt                   
                        pytest -v -o junit_family=xunit1 --cov=. --cov-report xml:coverage.xml --junitxml=nosetests.xml
                        deactivate
                   '''    
                   */

                   echo "Perform Unit Test"
            }
                    // post success publish test result using  Warnings Next Generation plugin
/*            post {
                success {
                         recordIssues(tools: [junitParser(pattern: 'nosetests.xml')])
                }
               
            }
            */
        }
                    // Scanning source code using sonarqube scannerand pubilsh reports to sonar server
        stage('Dev-PublishToSonarQube') {
            when {
                branch 'dev'
            }
            steps {
         /*      withSonarQubeEnv('sonarserver') {
            sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=email-notification \
            -Dsonar.sources=RabbitMQ_Consumer/ \
            -Dsonar.python.flake8.reportPaths=flake8-out.txt \
           # -Dsonar.python.xunit.reportPath=nosetests.xml \
           # -Dsonar.python.coverage.reportPaths=coverage.xml 
           # -Dsonar.tests=RabbitMQ_Consumer/ConsumerEx/ \
          # -Dsonar.python.xunit.skipDetails=false \
           '''
           */
           echo "hello"
            } 
                // abourt job if QualityGate fail.
            /*
                timeout(time: 10, unit: 'MINUTES') {
                     waitForQualityGate abortPipeline: true
                }  
            } */

        }
    // Build and push docker images for dev env
        stage('Dev-BuildDockerImage') {
            when {
                branch 'dev'
             beforeAgent true
            }
            agent {label 'slave'}
            options { skipDefaultCheckout() }
                       
            steps {              
                  //calling fucntion to build and push docker imagesjfjfj
                imageBuild(dev,imageName,Tags)
                    withCredentials([usernamePassword(credentialsId: 'nexus-repo', passwordVariable: 'dockerPassword', usernameVariable: 'dockerUser')]) {
                     pushToImage(registry,dev,imageName, dockerUser, dockerPassword,Tags)
                    deleteImages(registry,dev,imageName,Tags)
                   
                }
            }

        }
// deploy dev application on kubernets
        stage('Dev-Deploy') {
            when {
                branch 'dev'
            }
            steps {
                 sh "chmod +x deployment/changeVariable.sh"
                     sh "./deployment/changeVariable.sh $registry $dev-$imageName $BUILD_NUMBER 30000 dev"
                     sshagent(['ssh-agent']) {
                    sh "scp -o StrictHostkeyChecking=no deployment/dev-email-notification.yaml deployment/dev-rabbitmq-deploy.yaml ubuntu@192.168.0.20:/home/ubuntu/deployment/"
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/dev-rabbitmq-deploy.yaml -n=dev"  
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/dev-email-notification.yaml -n=dev"                    
                }
            }
        }

        stage('BuildDockerImage') {
            when {
                branch 'main'
             beforeAgent true
            }
            agent {label 'slave'}
                                   
            steps {              
                  //calling fucntion to build and push docker imagesjfjfj
                imageBuild('',imageName,versionTags)
                    withCredentials([usernamePassword(credentialsId: 'nexus-repo', passwordVariable: 'dockerPassword', usernameVariable: 'dockerUser')]) {
                     pushToImage(registry,'',imageName, dockerUser, dockerPassword,versionTags)
                    deleteImages(registry,'',imageName,versionTags)
                   
                }
            }

        }


    }    
 // This post stage run always and send email wih job status   
        post {
            always {
      //Sending email along with build details and log using shared lib function
            // emailnotify()
            echo "hello"
            }
        }    
}

// define function to build docker images
void imageBuild(env,imageName,Tags) {
    
    sh "docker build --rm -t $registry/$env$imageName:$Tags --pull --no-cache . -f $imageName'Dockerfile'"
    echo "Image build complete"
}

// define function to push imagesa
void pushToImage(registry,env,imageName, dockerUser, dockerPassword,Tags) {
    
    sh "docker login $registry -u $dockerUser -p $dockerPassword" 
    //sh "docker tag $env-$imageName:${BUILD_NUMBER} $registry/$env-$imageName:${BUILD_NUMBER}"
    //sh "docker tag $registry/$env$imageName:$Tags $registry/$env$imageName:latest"
    sh "docker push $registry/$env$imageName:$Tags"
    echo "Image Push $registry/$env$imageName:$Tags cpmoleted"
    //sh "docker push $registry/$env$imageName:latest"
    //echo "Image Push $registry/$env$imageName:latest cpmoleted"
    
}
void deleteImages(registry,env,imageName,Tags) {
    //sh "docker rmi $registry/$env$imageName:latest"
    sh "docker rmi $registry/$env$imageName:$Tags"
    echo "Images deleted"
    
}   

//read versionTag
void versiontags() {
   def tag= sh script: 'cat versionTags |tail -1', returnStdout: true
   return tag


}