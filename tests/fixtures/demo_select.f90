      subroutine demo_select (level)

      use demo_module

      implicit none

      character(len=*), intent (in) :: level   !! select level
      integer :: i                             !! counter
      real :: val = 0.                         !! result value

      do i = 1, 10
        select case (level)
        case ("low")
          val = val + i
        case ("mid")
          val = val - i
        case ("high")
          val = val * i
        case default
          val = 0.
        end select
      end do

      return
      end subroutine demo_select
