import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    this_dir = os.path.dirname(os.path.abspath(__file__))
    robot_xacro = os.path.join(this_dir, 'robot.urdf.xacro')
    controllers_file = os.path.join(this_dir, 'controllers.yaml')

    robot_description = Command([
        'xacro ',
        robot_xacro,
        ' use_ros2_control:=',
        use_ros2_control,
    ])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        )
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-entity', 'diff_bot', '-topic', 'robot_description'],
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
            '--param-file',
            controllers_file,
        ],
        condition=IfCondition(use_ros2_control),
    )

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
            '--param-file',
            controllers_file,
        ],
        condition=IfCondition(use_ros2_control),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='false',
            description='true: usar ros2_control, false: usar plugin DiffDrive clásico de Gazebo',
        ),
        gazebo,
        robot_state_publisher,
        spawn_robot,
        joint_state_broadcaster_spawner,
        diff_drive_controller_spawner,
    ])
