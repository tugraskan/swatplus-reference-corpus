      module demo_module

      implicit none

      integer :: basin_count = 0        !! number of basins
      real :: total_area = 0.           !! ha | total basin area

      type demo_state
        real :: flow = 0.               !! m3/s | current flow
        real :: stor = 0.               !! m3   | storage
      end type demo_state

      type (demo_state), dimension(:), allocatable :: dstate

      contains

      subroutine demo_zero (ds)
        type (demo_state), intent (inout) :: ds
        ds%flow = 0.
        ds%stor = 0.
      end subroutine demo_zero

      end module demo_module
