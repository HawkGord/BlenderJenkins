pipeline {
    agent { label 'First' }

    parameters {
        string(defaultValue: "C:/Jen/test.blend", description: 'Scene path', name: 'Scene')
        choice(choices: ['Sphere', 'Cube'], description: 'Object type', name: 'Object')
        string(defaultValue: "[${Math.random().round(1)},${Math.random().round(1)},${Math.random().round(1)},1]", description: 'Scene path', name: 'Color')
        choice(choices: ['png', 'jpg'], description: 'Image format', name: 'Image')
    }

    stages {
        stage("foo") {
            steps {
                bat "py C:/Jen/run_blender.py ${params.Scene} ${params.Object} ${params.Color} ${params.Image}"
            }
        
    	    post {
                success {
                    archiveArtifacts "render_img.${params.Image}"
                    archiveArtifacts 'run_blender_result.json'
                    archiveArtifacts 'log.txt'
                }
            }
        }
    }
}