pipeline{
    agent any
    environment{ 
        dockerImage = "ravikharel/compose"
    }
    stages{
        stage('Building the image'){ 
            steps{ 
                script{ 
                    sh "docker image build -t ${dockerImage}:${BUILD_NUMBER} ."
                }
            }
            
        }
        stage('Scanning the image'){ 
            steps{ 
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed $dockerImage:$BUILD_NUMBER'
            }
        }

        
        stage('Pushing the docker image to the docker hub'){ 
            steps{ 
                withDockerRegistry([credentialsId: 'docker-hub' , url: '']){

                sh '''
                docker push ${dockerImage}:${BUILD_NUMBER}
                '''
                }
                
            }
        }
        stage('Playing the playbook'){ 
            agent{ 
                label "ansible-node"
            }
            steps{ 
                sh '''
                    cd $WORKSPACE
                    ansible-playbook playbook.yml -e "workspace=$WORKSPACE" -e "number=$BUILD_NUMBER" -e "dockerImage=$dockerImage"

                '''
            }
        }
    }
}