      subroutine demo_calc (frac)

      use demo_module
      use time_module, only : yrs_print

      implicit none

      real, intent (in) :: frac      !! none | fraction applied to storage
      integer :: j                   !! counter
      real :: wrk = 0.               !! working value
      integer :: eof = 0

      open (107, file = "demo.in")
      read (107,*,iostat=eof) wrk
      close (107)

      do j = 1, basin_count
        call demo_zero (dstate(j))
        wrk = wrk + dstate(j)%stor * frac
      end do
      total_area = wrk

      return
      end subroutine demo_calc
