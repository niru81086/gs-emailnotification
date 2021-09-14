#!/usr/bin/env groovy   
@Library('myshared-library')_

 pipeline {
// define global agent
    agent {label 'master'}

 
// define environment variable 
        environment {
            scannerHome = tool 'sonar4.6'
            imageName = "email-consumer"
            qa= 'qa'
            stage= 'stage'
            dev= 'dev'
            registryCredentials = "Nexus"
            registry = "192.168.0.5:8050"
            dockerStageImage = ''
            dockerQAImage = ''
            versionTags= versiontags()
            
        }
 // This stage perform flake8 analysis when there is any new commit on dev branch dd          
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
               withSonarQubeEnv('sonarserver') {
            sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=email-notification \
            -Dsonar.sources=RabbitMQ_Consumer/ \
            -Dsonar.python.flake8.reportPaths=flake8-out.txt \
           # -Dsonar.python.xunit.reportPath=nosetests.xml \
           # -Dsonar.python.coverage.reportPaths=coverage.xml 
           # -Dsonar.tests=RabbitMQ_Consumer/ConsumerEx/ \
          # -Dsonar.python.xunit.skipDetails=false \
           '''
            } 
                // abourt job if QualityGate fail.
            
                timeout(time: 10, unit: 'MINUTES') {
                     waitForQualityGate abortPipeline: true
                }
            }

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
                  //calling fucntion to build and push docker images
                imageBuild(dev,imageName)
                withCredentials([usernamePassword(credentialsId: 'nexus-repo', passwordVariable: 'dockerPassword', usernameVariable: 'dockerUser')]) {
                     pushToImage(registry,dev,imageName, dockerUser, dockerPassword)
                     deleteImages(registry,dev,imageName)
                }
            }

        }
// deploy dev application on kubernets
        stage('Dev-Deploy') {
            when {
                branch 'dev'
            }
            steps {
                sshagent(['ssh-agent']) {
                    sh "scp -o StrictHostkeyChecking=no deployment/email-notification.yaml deployment/rabbitmq-deploy.yaml ubuntu@192.168.0.20:/home/ubuntu/deployment/"
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/rabbitmq-deploy.yaml -n=dev"  
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/email-notification.yaml -n=dev"                    
 
                }

            }

        }
// Build and push docker images for QA env This stage execute when there is new commit and dev branch merge t QA
        stage('QA-BuildImage') {
            when {
                branch 'qa'
                beforeAgent true
            }
            agent {label 'slave'}
            
            // to skip deafult beahviure of checkout   
    
            steps {
                /*    script {
                dockerQAImage = docker.build imageName
                    docker.withRegistry( 'http://'+registry, registryCredentials ) {
                         dockerQAImage.push('latest')
                        dockerQAImage.push('${BUILD_NUMBER}')
                    }
                } */
              
                    imageBuild(qa,imageName)
                    withCredentials([usernamePassword(credentialsId: 'nexus-repo', passwordVariable: 'dockerPassword', usernameVariable: 'dockerUser')]) {
                        pushToImage(registry,qa,imageName, dockerUser, dockerPassword)
                        deleteImages(registry,qa,imageName)
                    }                                 
            }
        }
// Deploy application on QA env This stage execute when there is new commit and dev branch merge to .
        stage('QA-Deploy') {
            when {
                branch 'qa'
                beforeAgent true
            }
            agent {label 'slave'}
            
            // to skip deafult beahviure of checkout   
    

            steps {
                    sh'''#/bin/bash -x
                    
                    "sed  's/imagename/$registry\\/$qa/g'  deployment/email-notification.yaml >  deployment/qa-email-notification.yaml"
                    '''
                     sshagent(['ssh-agent']) {
                    sh "scp -o StrictHostkeyChecking=no deployment/email-notification.yaml deployment/rabbitmq-deploy.yaml ubuntu@192.168.0.20:/home/ubuntu/deployment/"
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/rabbitmq-deploy.yaml -n=dev"  
                    sh "ssh ubuntu@192.168.0.20 kubectl apply -f deployment/email-notification.yaml -n=dev"                    
 
                }
            }

        }
            // This stage perform Selenuim test cases
        stage('QA-Selenimumtest') {
            when {
                beforeAgent true
                branch 'qa'
            }
                // define agent to run stage on specific agent           
          agent {label 'slave'}
            options { skipDefaultCheckout() }   
            // to skip deafult beahviure of checkout   
            steps {

                // Below code create selenuim and python container and execute selenium pytest code on pyton container 
             sh'''#!/bin/bash -x
                
            CONTAINER_selenium=$(docker run -d --name selenium -p 4444:4444 selenium/standalone-chrome)
            CONTAINER_python=$(docker run -d -t -e PYTHONUNBUFFERED=0 -w /root -v $WORKSPACE:/root --link selenium:selenium --name python python:3.7 /bin/bash)
            docker exec -i $CONTAINER_python /bin/bash -x -c "pip install -r requirements.txt &&  pytest -v -s --alluredir="Testcases/allureReport" -c Testcases/pytest.ini"
            docker logs $CONTAINER_python
            docker stop $CONTAINER_python $CONTAINER_selenium
            docker rm $CONTAINER_python $CONTAINER_selenium
            '''             }
                    // post success above steps publish allure report using allure plugin
                post {
                    success {
                        allure includeProperties: false, jdk: '', results: [[path: 'Testcases/allureReport']]
                    }
                }    
        } 
            // Build and push docker images for Stage env This stage execute when there is new commit  QA branch merge to Master    
        stage('Staging-BuildImage') {
            when {
                beforeAgent true
                branch 'stage'
            }           
           agent {label 'slave'}  
            steps {
                sh "docker login 192.168.0.5:8050 -u admin -p niru@123"
                sh "docker pull 192.168.0.5:8050/$qa-$imageName:latest"
                sh "docker tag 192.168.0.5:8050/$qa-$imageName:latest 192.168.0.5:8050/$stage-$imageName:$versionTags" 
                sh "docker push 192.168.0.5:8050/$stage-$imageName:$versionTags"              
                    echo "$versionTags"
                    echo "${versionTags}"                       
            }
        }
    // This stage wait for approval and once approve application deploy on stage env ss 
        stage('Staging-Deploy') {
            when {
                beforeAgent true
                branch 'master'
            }           
           
            steps {
                    // Wating for approval
                    input 'Prod deployment?'
            }
        }

        stage('Prod-Deploy') {
            when {
                beforeAgent true
                branch 'master'
            }
                                    
            steps {
                        // waiting for approval        
                input 'Prod deployment?'
                        // deploy on production
                     //calling 
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
void imageBuild(env,imageName) {

    sh "docker build --rm -t $env-$imageName:${BUILD_NUMBER} --pull --no-cache . -f $imageName'Dockerfile'"
    echo "Image build complete"
}

// define function to push imagesa
void pushToImage(registry,env,imageName, dockerUser, dockerPassword) {
    
    sh "docker login $registry -u $dockerUser -p $dockerPassword" 
    sh "docker tag $env-$imageName:${BUILD_NUMBER} $registry/$env-$imageName:${BUILD_NUMBER}"
    sh "docker tag $env-$imageName:${BUILD_NUMBER} $registry/$env-$imageName:latest"
    sh "docker push $registry/$env-$imageName:${BUILD_NUMBER}"
    echo "Image Push $registry/$env-$imageName:${BUILD_NUMBER} cpmoleted"
    sh "docker push $registry/$env-$imageName:latest"
    echo "Image Push $registry/$env-$imageName:latest cpmoleted"
    
}
void deleteImages(registry,env,imageName) {
    sh "docker rmi $registry/$env-$imageName:latest"
    sh "docker rmi $registry/$env-$imageName:${BUILD_NUMBER}"
    echo "Images deleted"
    
}   

//read versionTag
void versiontags() {
   def tag= sh script: 'cat versionTags |tail -1', returnStdout: true
   return tag


}