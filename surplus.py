  # Check if we are on a direct crash course towards the object by forming
  # rectangles and inspecting their aspect ratios
  # x----|-------|
  # |    |       |
  # | A  |       |
  # -----x-------|
  # |    |       |
  # |    | B     |
  # |    |       |
  #--------------x
  # If rectangle A has the same aspect ratio as rectangle B, then we are on a
  # direct crash course
  ship_cock_x = a.x - a.rect.bottomright[0]
  ship_cock_y = a.y - a.rect.bottomright[1]
  ship_center_to_cock = pygame.Rect(a.x, a.y, ship_cock_x, ship_cock_y)
  ship_cock_to_object = pygame.Rect(ship_cock_x, ship_cock_y, b.x, b.y)
  center_cock_ratio = ship_center_to_cock.width / ship_center_to_cock.height
  cock_object_ratio = ship_cock_to_object.width / ship_cock_to_object.height

  print "CCW " + str( ship_center_to_cock.width)
  print "CCH " + str(  ship_center_to_cock.height)
  print "COW " + str(  ship_cock_to_object.width )
  print "COH " + str(  ship_cock_to_object.height )
