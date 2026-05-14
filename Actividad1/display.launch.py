from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('dif_bot_description')

    robot_description = Command([
        'xacro ',
        PathJoinSubstitution([pkg_share, 'urdf', 'robot.urdf.xacro'])
    ])

    rviz_config = PathJoinSubstitution([pkg_share, 'rviz', 'urdf_config.rviz'])

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config]
        )
    ])
